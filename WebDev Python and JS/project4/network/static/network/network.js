document.addEventListener("DOMContentLoaded", function () {

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

    fetch("/load_allposts")
        .then((response) => response.json())
        .then((posts) => {

            posts.forEach((item) => {
                console.log(item);
                // build posts
                build_posts(item);
                // click event to bring full post
                // document.querySelector("#allposts-div").appendChild(parent_element);
            })
        })
}


function getLikes(postid, color) {
    //console.log(color);
    // color.style.color = "red";
    fetch("/likes", {
        method: 'POST',
        body: postid,
    }).then(response => response.json());
    // Not very elegant, but...
    window.location.reload();
    // document.getElementById("megusta").innerHTML = document.getElementById("megusta").innerHTML;
}
function editpost(postid, x) {
    alert(postid);

}

// TODO SPLIT THIS FUNCTION
// is getting too big
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
    num_likes.id = "megusta";
    // console.log(num_likes.id);
    const date = document.createElement("div");
    date.classList = "date";

    // Date.
    date.innerHTML = `Posted on: ${item["posted_on"]}`;
    // <a href="{% url 'user_profile' username=user.username  %}"> Profile</a>
    // User
    const posterlink = item["poster"];
    // This is the only way I could pass a var to DJango
    // Maybe is a better way?
    poster.innerHTML = `<a href="/user_profile/${posterlink}">` + posterlink + '</a>';
    poster_avatar.classList = "post_avatar";
    poster_avatar.innerHTML = ' <img src="static/network/profile.png" />';

    postheader.appendChild(date);
    postheader.appendChild(poster_avatar);
    postheader.appendChild(poster);



    // Body
    body.innerHTML = `<h3> ${item["content"]} </h3>`;
    // content.appendChild(body);

    // Like button

    //if (item["is_liked"]) {
    like_button.innerHTML = '<i class="material-icons-outlined" style="color:red" onclick="getLikes(\'' + `${item.id}` + '\', this)"> favorite_border</i>';
    //} else {
    // like_button.innerHTML = '<i class="fa fa-heart" aria-hidden="true" onclick="getLikes(\'' + `${item.id}` + '\', \'' + `${item.num_likes}` + '\')" ></i>';
    //}


    like_button.classList = "like-button";
    // like_button.style = "color:red";


    // TODO add click event to add likes to DB and change the button to filled && update DB

    num_likes.innerHTML = item["num_likes"];
    num_likes.className = "likes";

    // Edit post
    const editlink = document.createElement("div");
    editlink.id = "edit_link";
    editlink.innerHTML = '<i onclick="editpost(\'' + `${item.id}` + '\', this)" class="fas fa-edit"></i>';
    editlink.className = "edit";

    // Post footer
    postfooter.appendChild(like_button);
    postfooter.appendChild(num_likes);
    postfooter.appendChild(editlink);

    // Build posts

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