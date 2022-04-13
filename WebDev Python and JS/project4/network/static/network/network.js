document.addEventListener("DOMContentLoaded", function () {
    // Use buttons to toggle between views
    // document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
    // document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
    // document.querySelector("#archived").addEventListener("click", () => load_mailbox("archive"));
    // document.querySelector("#compose").addEventListener("click", compose_email);
    // Add event listener to the form
    document.querySelector("#compose-form").addEventListener("submit", submit_post);

    // By default, load all posts
    load_allposts();
});

function submit_post(event) {
    event.preventDefault();
    const post = document.querySelector("#add-post").value;

    // Send post to server
    fetch("/create_post", {
        method: "POST",
        body: JSON.stringify({ post: post }),

    })
        .then((response) => response.json())
    load_allposts();

    document.querySelector("#add-post").value = "";
}

function load_allposts() {
    console.log("inside all psots");
    fetch("/load_allposts")
        .then((response) => response.json())
        .then((posts) => {
            posts.forEach((item) => {
                const parent_element = document.createElement("div");
                // build posts
                build_posts(item, parent_element);
                // click event to bring full post
                document.querySelector("#allposts-div").appendChild(parent_element);
            })
        })
}



function build_posts(item, parent_element) {
    const content = document.createElement("div");
    // Set and style the date.
    const date = document.createElement("div");
    date.innerHTML = item["posted_on"];
    date.style.display = "inline-block";
    date.style.float = "right";

    content.appendChild(date);
    content.style.padding = "10px";

    parent_element.appendChild(content);



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