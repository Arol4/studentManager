window.addEventListener('load', adjustTextSize);
window.addEventListener('resize', adjustTextSize);

function adjustTextSize() {
    const containers = document.querySelectorAll('.descriptionImage');
    containers.forEach(container => {
        const p = container.querySelector('p');
        let fontSize = 1;
        p.style.fontSize = fontSize + 'px';
        
        while (p.scrollHeight <= container.clientHeight && fontSize < 200) {
            fontSize++;
            p.style.fontSize = fontSize + 'px';
        }
        p.style.fontSize = (fontSize - 1) + 'px';
    });
}