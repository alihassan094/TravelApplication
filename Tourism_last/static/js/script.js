const navbar = document.getElementsByClassName('navbar')[0];
// document.querySelector('#menu-btn').onclick = () =>{
//     navbar.classList.toggle('active');
// }
document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('#menu-btn');
    button.onclick = function() {
        // your code here
        navbar.classList.toggle('active');
    };
});

window.onscroll = () =>{
    navbar.classList.remove('active');
}

document.querySelectorAll('.about .video-container .controls .control-btn').forEach(btn =>{
    btn.onclick = () =>{
        let src = btn.getAttribute('data-src');
        document.querySelector('.about .video-container .video').src = src;
    }
})