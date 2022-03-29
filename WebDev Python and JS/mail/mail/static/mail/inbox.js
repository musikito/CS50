document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document.querySelector("#inbox").addEventListener("click", () => load_mailbox("inbox"));
  document.querySelector("#sent").addEventListener("click", () => load_mailbox("sent"));
  document.querySelector("#archived").addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);
  // Add event listener to the form
  document.querySelector("#compose-form").addEventListener("submit", send_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function send_email(event) {

  event.preventDefault();

  // Get the required fields.
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  // Send the data to the server.
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    // Take the return data and parse it in JSON format.
    .then((response) => response.json())
    .then((result) => {
      load_mailbox("sent", result);
    })

}

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox, message = "") {
  // Delete any messages if any
  document.querySelector("#message-div").textContent = "";

  // Print a message if any.
  if (message !== "") {
    make_alert(message);
  }

  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get data of the corresponding mailbox from the server.
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((item) => {

        const parent_element = document.createElement("div");

        build_emails(item, parent_element, mailbox);

        parent_element.addEventListener("click", () => read_email(item["id"]));
        document.querySelector("#emails-view").appendChild(parent_element);

      });
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


function build_emails(item, parent_element, mailbox) {
  if (mailbox === "inbox" && item["archived"]) {
    return;
  }
  else if (mailbox === "archive" && !item["archived"]) {
    return;
  }

  const content = document.createElement("div");

  const recipients = document.createElement("strong");
  if (mailbox === "sent") {
    recipients.innerHTML = item["recipients"].join(", ") + " ";
  }
  else {
    recipients.innerHTML = item["sender"] + " ";
  }
  content.appendChild(recipients);

  content.innerHTML += item["subject"];

  // Set and style the date.
  // Was tricky, it was giving a bad styling
  const date = document.createElement("div");
  date.innerHTML = item["timestamp"];
  date.style.display = "inline-block";
  date.style.float = "right";

  if (item["read"]) {
    parent_element.style.backgroundColor = "grey";
    date.style.color = "black";
  } else {
    // date.className = "text-muted";
    parent_element.style.backgroundColor = "white";
    date.style.color = "black";
  }
  content.appendChild(date);

  content.style.padding = "10px";
  parent_element.appendChild(content);


  // Style the parent element.
  parent_element.style.borderStyle = "solid";
  parent_element.style.borderWidth = "3px";
  parent_element.style.margin = "10px";
}

function read_email(id) {
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "block";

  // Erase any email that was here
  document.querySelector("#email-view").innerHTML = "";

  // Get the email's info and build the section.
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(result => {
      build_email(result);
    })
    .catch(error => console.log(error));

  // Set the email to read.
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  });
}

function build_email(data) {
  const from = document.createElement("div");
  const to = document.createElement("div");
  const subject = document.createElement("div");
  const timestamp = document.createElement("div");
  const reply_button = document.createElement("button");
  const archive_button = document.createElement("button");
  const body = document.createElement("div");

  from.innerHTML = `<strong>From: </strong> ${data["sender"]}`;
  to.innerHTML = `<strong>To: </strong> ${data["recipients"].join(", ")}`;
  subject.innerHTML = `<strong>Subject: </strong> ${data["subject"]}`;
  timestamp.innerHTML = `<strong>Timestamp: </strong> ${data["timestamp"]}`;
  body.innerHTML = data["body"];

  // * Archive button
  archive_button.innerHTML = '<i class="fa fa-archive" aria-hidden="true">';
  if (data["archived"]) {
    archive_button.innerHTML += "Unarchive";
  } else {
    archive_button.innerHTML += "Archive";
  }
  archive_button.classList = "btn btn-outline-primary m-2";
  archive_button.addEventListener("click", () => {
    archive_email(data);
    load_mailbox("inbox");
  });

  // * Reply button
  reply_button.innerHTML = '<i class="fa fa-reply" aria-hidden="true"></i> Reply';
  reply_button.classList = "btn btn-outline-primary m-2";
  reply_button.addEventListener("click", () => compose_reply(data));

  document.querySelector("#email-view").appendChild(from);
  document.querySelector("#email-view").appendChild(to);
  document.querySelector("#email-view").appendChild(subject);
  document.querySelector("#email-view").appendChild(timestamp);
  document.querySelector("#email-view").appendChild(archive_button);
  document.querySelector("#email-view").appendChild(reply_button);
  document.querySelector("#email-view").appendChild(document.createElement("hr"));
  document.querySelector("#email-view").appendChild(body);
}

function archive_email(data) {
  fetch(`/emails/${data["id"]}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: !data["archived"]
    })
  });
}

function compose_reply(data) {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = data["sender"];
  document.querySelector("#compose-subject").value = ((data["subject"].match(/^(Re:)\s/)) ? data["subject"] : "Re: " + data["subject"]);
  document.querySelector("#compose-body").value = `On ${data["timestamp"]} ${data["sender"]} wrote:\n${data["body"]}\n-------------------------------------\n`;
}