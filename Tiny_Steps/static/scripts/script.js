// const button = document.querySelector('.gh1');

// button.addEventListener('click', event => {
//     fetch('/pay')
//     .then(result => { return result.json(); })
//     .then(data => {
//         var stripe = Stripe(data.checkout_public_key);

//         stripe.redirectToCheckout({
//             sessionId: data.checkout_session_id
//         }).then(result => {})
//     })
// });

function test(priceid) {
    fetch(`/pay?priceid=${priceid}`)
    .then(result => { return result.json(); })
    .then(data => {
        var stripe = Stripe(data.checkout_public_key);
        console.log(data);

        stripe.redirectToCheckout({
            sessionId: data.checkout_session_id
        }).then(result => {})
    })
}

test(priceid);