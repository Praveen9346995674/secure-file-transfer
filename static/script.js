// auto-hide alerts
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        alert.style.opacity = "0";
        alert.style.transition = "0.5s";
    });
}, 3000);

// smooth fade
window.onload = () => {
    document.body.style.opacity = 0;
    setTimeout(() => {
        document.body.style.transition = "0.6s";
        document.body.style.opacity = 1;
    }, 100);
};