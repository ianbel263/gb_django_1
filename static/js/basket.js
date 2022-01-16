'use strict';

const SERVER_TIMEOUT = 15000
const cookie = document.cookie
const csrfToken = cookie.substring(cookie.indexOf('=') + 1)

const RequestMethod = {
    GET: `GET`,
    POST: `POST`,
    PUT: `PUT`,
    DELETE: `DELETE`
};

const Urls = {
    ADD: '/basket/add/',
    UPDATE: '/basket/update/'
};

const debounce = (f, ms) => {
  let timer = null;
  return function (...args) {
    const onComplete = () => {
      f.apply(this, args);
      timer = null;
    }
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(onComplete, ms);
  };
};

const checkStatus = (response) => {
    if (response.status >= 200 && response.status < 300) {
        return response;
    } else {
        throw new Error(`${response.status}: ${response.statusText}`);
    }
};

const load = ({url, method = RequestMethod.GET, body = null, headers = new Headers()}) => {
    return Promise.race([
        fetch(`${url}`, {method, body, headers}),
        new Promise((resolve) => setTimeout(resolve, SERVER_TIMEOUT))
    ])
        .then(checkStatus)
        .catch((err) => {
            throw err;
        });
};

const onAddBasketLinkClick = (evt) => {
    evt.preventDefault();
    const productID = evt.target.dataset.id
    const uploadData = {
        productID: productID
    }
    const url = `${Urls.ADD}${productID}/`
    load({
        url: url,
        method: RequestMethod.POST,
        headers: new Headers({
            'X-CSRFToken': csrfToken,
            'Content-Type': `application/json`
        }),
        body: JSON.stringify(uploadData),
    })
        .then((response) => {
            if (response.redirected) {
                window.location.href = response.url
                throw 'redirect'
            }
            return response.json()
        })
        .then((data) => {
            if (data.success) {
                alert('Товар добавлен в корзину');
            }
        })
        .catch((error) => {
            console.log(error)
        });
};

const onProductQuantityChange = (evt, elements) => {
    const {priceEl, totalPriceEl, totalQuantityEl} = elements;
    const uploadData = {
        basketID: evt.target.dataset.id,
        quantity: evt.target.value
    }
    load({
        url: Urls.UPDATE,
        method: RequestMethod.POST,
        body: JSON.stringify(uploadData),
        headers: new Headers({
            'X-CSRFToken': csrfToken,
            'Content-Type': `application/json`
        })
    })
        .then(response => response.json())
        .then((data) => {
            evt.target.defaultValue = data.quantity;
            evt.target.value = data.quantity;
            priceEl.textContent = `${data.price} руб.`;
            totalPriceEl.textContent = `${data.totalPrice} руб.`;
            totalQuantityEl.textContent = data.totalQuantity;
        })
        .catch((error) => {
            evt.target.value = evt.target.defaultValue;
            alert(`Вы превышаете остаток товара в магазине.`);
        })
}

const addBasketLinks = document.querySelectorAll('#add_basket');
if (addBasketLinks) {
    addBasketLinks.forEach(link => {
        link.addEventListener('click', onAddBasketLinkClick);
    });
}

const debouncedProductChange = debounce(onProductQuantityChange, 500);

const basket = document.querySelector('#basket')
if (basket) {
    const elements = {
        totalPriceEl: basket.querySelector('#total_price'),
        totalQuantityEl: basket.querySelector('#total_quantity')
    }
    const quantityFields = basket.querySelectorAll('input[name="basketID"]');
    quantityFields.forEach(field => {
        elements.priceEl = field.parentNode.parentNode.querySelector('#price');
        field.addEventListener('change', (evt) => debouncedProductChange(evt, elements));
    });
}
