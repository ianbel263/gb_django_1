'use strict';

const onFileSelect = (evt) => {
    const file = evt.target.files;
    const f = file[0];
    const reader = new FileReader();
    reader.onload = (function (theFile) {
        return function (e) {
            const labelEl = evt.target.parentNode.querySelector('label');
            const imgEl = document.querySelector('#img_preview').querySelector('img');
            labelEl.textContent = theFile.name;
            imgEl.src = e.target.result;
        };
    })(f);
    reader.readAsDataURL(f);
}

const fileInput = document.querySelector('input[id=id_image]');
if (fileInput) {
    fileInput.addEventListener('change', onFileSelect, false);
}
