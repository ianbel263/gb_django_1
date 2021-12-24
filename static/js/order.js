'use strict';

// const totalFormNumber = document.querySelector('input[name=order_items-TOTAL_FORMS]').value;
// const initialFormNumber = document.querySelector('input[name=order_items-INITIAL_FORMS]').value;

class Order {
    constructor() {
        this.products = [];
        this.formsetRows = document.querySelectorAll('.formset_row');
    }

    init() {
        if (this.formsetRows) {
            this.formsetRows.forEach(row => {
                this._addListeners(row);
                this._findProducts(row);
            });
        }
    }

    getProducts() {
        return this.products;
    }

    _updateProducts(id, quantity, pricePerOne) {
        let isAdded = false;
        this.products.forEach(product => {
            if (product.id === id) {
                product.quantity = quantity;
                isAdded = true;
            }
        });
        if (!isAdded) {
            this.products.push({
                id: id,
                quantity: quantity,
                pricePerOne: pricePerOne
            });
        }
    }

    _findProducts(formsetRow) {
        const elements = this._getRowElements(formsetRow)
        const {productIdEl, productEl, quantityEl, _} = elements
        if (productEl.options.selectedIndex !== 0) {
            this.products.push({
                id: productIdEl.value,
                quantity: parseInt(quantityEl.value),
                pricePerOne: this._getPricePerOne(elements)
            });
        }
    }

    _addListeners(formsetRow) {
        const elements = this._getRowElements(formsetRow)
        const {productIdEl, productEl, quantityEl, priceEl} = elements
        if (productEl.options.selectedIndex !== 0) {
            const pricePerOne = this._getPricePerOne(elements)
            quantityEl.addEventListener('change', evt => {
                this._onQuantityChange(evt, pricePerOne, priceEl);
                this._updateProducts(productIdEl.value, +quantityEl.value, pricePerOne);
                this._updateSummary();
            });
        }
    }

    _onQuantityChange(evt, pricePerOne, priceEl) {
        if (evt.target.value < 1) {
            evt.target.value = 1;
        }
        const newPrice = Math.round(pricePerOne * evt.target.value * 100) / 100;
        priceEl.textContent = newPrice.toFixed(2).toString();
    }

    _getRowElements(formsetRow) {
        return {
            productIdEl: formsetRow.querySelector('input[name$=product_id]'),
            productEl: formsetRow.querySelector('select'),
            quantityEl: formsetRow.querySelector('input[type=number]'),
            priceEl: formsetRow.querySelector('span[class$=price]')
        }
    }

    _getPricePerOne(elements) {
        const {_, __, quantityEl, priceEl} = elements;
        const totalPrice = parseFloat(priceEl.textContent.replace(',', '.')).toFixed(2);
        const quantity = parseInt(quantityEl.value);
        return Math.round(totalPrice / quantity * 100) / 100;
    }

    _getTotalQuantity() {
        return this.products.reduce((acc, product) => {
            acc += product.quantity;
            return acc;
        }, 0);
    }

    _getTotalPrice() {
        return this.products.reduce((acc, product) => {
            acc += product.quantity * product.pricePerOne;
            return acc;
        }, 0).toFixed(2);
    }

    _updateSummary() {
        const totalQuantityEl = document.querySelector('.order_total_quantity');
        const totalAllPriceEl = document.querySelector('.order_total_cost');
        if (totalQuantityEl && totalAllPriceEl) {
            totalQuantityEl.textContent = this._getTotalQuantity();
            totalAllPriceEl.textContent = this._getTotalPrice();
        }
    }
}

const order = new Order()
order.init()
