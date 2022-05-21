function load_user_posts() {
    fetch("/load_user_posts")
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

    document.querySelector("#allposts-div").appendChild(postheader);
    document.querySelector("#allposts-div").appendChild(body);
    document.querySelector("#allposts-div").appendChild(postfooter);
    document.querySelector("#allposts-div").appendChild(document.createElement("hr"));

}