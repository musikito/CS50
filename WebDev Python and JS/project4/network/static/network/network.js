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

                // build posts
                build_posts(item);
                // click event to bring full post
                // document.querySelector("#allposts-div").appendChild(parent_element);
            })
        })
}



function build_posts(item) {
    const content = document.createElement("div");
    content.classList = "post";
    const postheader = document.createElement("div");
    postheader.classList = "post_header";
    const postfooter = document.createElement("div");
    postfooter.classList = "post_footer";
    const poster = document.createElement("div");
    const poster_avatar = document.createElement("div");
    const body = document.createElement("div");
    body.classList = "body_text";
    const like_button = document.createElement("icon");
    const num_likes = document.createElement("div");
    const date = document.createElement("div");
    date.classList = "date";

    // Date.
    date.innerHTML = `Posted on: ${item["posted_on"]}`;

    // User
    poster.innerHTML = item["poster"];
    poster_avatar.classList = "post_avatar";
    poster_avatar.innerHTML = ' <img src="static/network/profile.png" />';

    postheader.appendChild(date);
    postheader.appendChild(poster_avatar);
    postheader.appendChild(poster);



    // Body
    body.innerHTML = `<h3> ${item["content"]} </h3`;
    content.appendChild(body);

    // Like button
    like_button.innerHTML = '<span class="material-icons-outlined"> favorite_border</span>';
    // TODO add click event to add likes to DB and change the button to filled && update DB

    num_likes.innerHTML = item["num_likes"];
    num_likes.style.float = "left";

    // Post footer
    postfooter.appendChild(like_button);
    postfooter.appendChild(num_likes);

    // Build posts
    // document.querySelector("#allposts-div").appendChild(poster);
    // document.querySelector("#allposts-div").appendChild(poster_avatar);
    // document.querySelector("#allposts-div").appendChild(date);
    // document.querySelector("#allposts-div").appendChild(like_button);
    // document.querySelector("#allposts-div").appendChild(num_likes);
    document.querySelector("#allposts-div").appendChild(postheader);
    document.querySelector("#allposts-div").appendChild(body);
    document.querySelector("#allposts-div").appendChild(postfooter);
    document.querySelector("#allposts-div").appendChild(document.createElement("hr"));


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