window.onload = function() {
    let images = document.getElementsByClassName("lazy");

    for (let i = 0; i < images.length; i++) {
       let image = images.item(i);
       let image_url = image.getAttribute('data-src');

       image.onload = function (_event) {
           this.classList.add('loaded');
       }
       image.setAttribute('src', image_url);
       image.removeAttribute('data-src');
    }
};
