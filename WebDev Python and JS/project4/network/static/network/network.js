document.addEventListener("DOMContentLoaded", function () {
    // Use buttons to toggle between views
    // document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
    // document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
    // document.querySelector("#archived").addEventListener("click", () => load_mailbox("archive"));
    // document.querySelector("#compose").addEventListener("click", compose_email);
    // Add event listener to the form
    document.querySelector("#compose-form").addEventListener("submit", submit_post);

    // By default, load all posts
    // load_page("posts");
});

function submit_post(event) {
    event.preventDefault();
    const post = document.querySelector("#add-post").value;

    // Send post to server
    fetch("/create_post", {
        method: "POST",
        body: JSON.stringify({ create_post: post }),

    })
        .then((response) => response.json())
        .then((result) => {
            console.log("submitted form", result);
        })


}

function make_alert(message) {
    const element = document.createElement("div");
    element.classList.add("alert");

    if (message["message"]) {
        element.classList.add("alert-success");
        element.innerHTML = message["message"];
    } else if (message["error"]) {
        element.classList.add("alert-danger");
        element.innerHTML = message["error"];
    }

    document.querySelector("#message-div").appendChild(element);
}