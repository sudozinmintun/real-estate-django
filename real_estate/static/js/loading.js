document.body.addEventListener("htmx:beforeRequest", function() {
    document.querySelector(".hx-progress").classList.add("active");
});

document.body.addEventListener("htmx:afterRequest", function() {
    const bar = document.querySelector(".hx-progress");
    bar.classList.remove("active");
});

document.body.addEventListener("htmx:responseError", function() {
    const bar = document.querySelector(".hx-progress");
    bar.classList.remove("active");
});