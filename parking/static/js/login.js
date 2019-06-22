//document.body.requestFullscreen();
window.scrollTo( 0, 1 );

const textfs = document.querySelectorAll('.mdc-text-field')

for (const textf of textfs) {
    mdc.textField.MDCTextField.attachTo(textf);
}


const buttons = document.querySelectorAll('.mdc-button');

for (const button of buttons) {
    mdc.ripple.MDCRipple.attachTo(button);
}
