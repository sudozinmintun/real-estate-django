const bar = document.querySelector(".hx-progress");

function startBar() {
    bar.style.opacity = "1";
    bar.style.width = "10%";
    let progress = 10;

    bar._interval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress < 90) bar.style.width = progress + "%";
    }, 300);
}

function finishBar() {
    bar.style.width = "100%";
    setTimeout(() => {
        bar.style.opacity = "0";
        bar.style.width = "0%";
        clearInterval(bar._interval);
    }, 400);
}

document.body.addEventListener("htmx:beforeRequest", startBar);
document.body.addEventListener("htmx:afterRequest", finishBar);
document.body.addEventListener("htmx:responseError", finishBar);
