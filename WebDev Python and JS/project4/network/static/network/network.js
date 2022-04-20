document.addEventListener("DOMContentLoaded", function () {
    // Use buttons to toggle between views
    // document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
    // document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
    // document.querySelector("#archived").addEventListener("click", () => load_mailbox("archive"));
    // document.querySelector("#compose").addEventListener("click", compose_email);

    // By default, load all posts
    load_allposts();
    // Add event listener to the form
    document.querySelector("#compose-form").addEventListener("submit", submit_post);


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
    // const content = document.createElement("div");
    const poster = document.createElement("div");
    const poster_avatar = document.createElement("div");
    const body = document.createElement("div");
    const like_button = document.createElement("button");
    const num_likes = document.createElement("div");
    const date = document.createElement("div");

    // Set and style the date.
    date.innerHTML = `<strong> Date: </strong> ${item["posted_on"]}`;
    date.style.display = "inline-block";
    date.style.float = "right";

    // Body
    body.innerHTML = item["content"];

    // User
    poster.innerHTML = item["poster"];
    poster_avatar.classList = "post_avatar";
    poster_avatar.innerHTML = ' <img src="static/network/profile.png" />';

    num_likes.innerHTML = item["num_likes"];

    // DEBUG
    console.log(item["content"]);
    console.log(item["poster"]);
    console.log(item["num_likes"]);

    // Like button
    like_button.innerHTML = '<span class="material-icons-outlined"> favorite_border</span>';
    like_button.classList = "btn btn-outline-primary m-2";
    // TODO add click event to add likes to DB and change the button to filled && update DB

    // Build posts
    document.querySelector("#allposts-div").appendChild(poster);
    document.querySelector("#allposts-div").appendChild(poster_avatar);
    document.querySelector("#allposts-div").appendChild(date);
    document.querySelector("#allposts-div").appendChild(like_button);
    document.querySelector("#allposts-div").appendChild(num_likes);
    document.querySelector("#allposts-div").appendChild(body);
    document.querySelector("#allposts-div").appendChild(document.createElement("hr"));




    // content.appendChild(date);
    // content.style.padding = "10px";

    // parent_element.appendChild(content);

    //Style the parent element
    parent_element.style.borderstyle = "solid";
    parent_element.style.borderwith = "3px";
    parent_element.style.margin = "10px";



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