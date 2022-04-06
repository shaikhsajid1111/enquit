/**
 * @author Akankshi Gupta <akankshigp12345@gmail.com>
 */
const makeRequest = async (url: string) => {
  try {
    const response: Response = await fetch(url);
    return await response.json();
  } catch (error) {
    console.log(`Error at makeRequest:  ${error.message}`);
    return null;
  }

}

const manipulate = (id: string, value: string): void => {
  document.getElementById(id).innerHTML = value;
}

const updateVoteCount = (id: string, upvote: boolean): void => {
  const vote_count_element: HTMLElement = document.getElementById(id);
  if (upvote) {
    const increment_count: number = parseInt(vote_count_element.innerHTML) + 1;
    vote_count_element.innerHTML = increment_count.toString();
  } else {
    const increment_count = parseInt(vote_count_element.innerHTML) - 1;
    vote_count_element.innerHTML = increment_count.toString();
  }
}

const toggleIcon = (id: string, icon_class_to_add: string, icon_class_to_remove: string): void => {
  try {
    const element: HTMLElement = document.getElementById(id);
    element.classList.remove(icon_class_to_remove);
    element.classList.add(icon_class_to_add);

  } catch (error) {
    console.error('Error at ToggleIcon  : ', error.message);
  }
}

const votePost = async (post_id: number) => {
  try {
    const url: string = `/api/vote_post/${post_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Voted the post!') {
      toggleIcon(`vote-${post_id}`, 'fa-check-circle', 'fa-check');
      updateVoteCount(`vote-count-${post_id}`, true);
    } else {
      toggleIcon(`vote-${post_id}`, 'fa-check', 'fa-check-circle');
      updateVoteCount(`vote-count-${post_id}`, false);

    }
  } catch (error) {
    console.log(`Error making request : ${error.message}`);
  }
}

const voteAnswer = async (answer_id: number) => {
  try {
    const url: string = `/api/vote_answer/${answer_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Voted the answer!') {
      toggleIcon(`answer-${answer_id}`, 'fa-check-circle', 'fa-check');
      updateVoteCount(`answer-vote-count-${answer_id}`, true);
    } else {
      toggleIcon(`answer-${answer_id}`, 'fa-check', 'fa-check-circle');
      updateVoteCount(`answer-vote-count-${answer_id}`, false);

    }
  } catch (error) {
    console.log(`Error making request : ${error.message}`);
  }
}

const updateSavedButton = (state: boolean, post_id: number) => {
  /**if the state is true means a new post was saved */
  const element_id: string = `saved-${post_id}`;
  const element: HTMLElement = document.getElementById(element_id);
  if (state == true) {
    element.innerHTML = 'Save';
  } else if (state == false) {
    /**else if the state is false, post have been unsaved */
    element.innerHTML = 'Unsave';
  }
}

const savePost = async (post_id: number) => {
  try {
    const url: string = `/api/save/${post_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Unsaved the answer!') {
      toggleIcon(`saved-${post_id}`, 'far', 'fas');
    } else {
      toggleIcon(`saved-${post_id}`, 'fas', 'far');
    }
  } catch (error) {
    console.warn(error.message);
  }
}


const reportPost = async (post_id: number) => {
  try {
    const url: string = `/api/report_post/${post_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Reported!') {
      toggleIcon(`report-post-${post_id}`, 'fas', 'far');
    }
  } catch (error) {
    console.error(`Error at Report Post : ${error.message}`);
  }
}

const reportAnswer = async (answer_id: number) => {
  try {
    const url: string = `/api/report_answer/${answer_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Reported!') {
      toggleIcon(`report-answer-${answer_id}`, 'fas', 'far');
    }
  } catch (error) {
    console.error(`Error at Report Answer : ${error.message}`);
  }
}

const reportAccount = async (account_id: number) => {
  try {
    const url: string = `/api/report_account/${account_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Reported!') {
      toggleIcon(`report-account-${account_id}`, 'fas', 'far');
    }
  } catch (error) {
    console.error(`Error at Report Account : ${error.message}`);
  }
}



const convertDateFormat = (date: string, id: string) => {
  const date_obj: Date = new Date(date);
  const time_string: string = date_obj.toDateString().toString().slice(4) + " at " + date_obj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  document.getElementById(id).innerHTML = time_string.toString();
}

const Validate = () => {
  const upload_element = document.getElementById("upload");
  for (let i = 0; i < upload_element.files.length; i++) {
    const filetype = upload_element.files.item(i).type;
    const file_size = upload_element.files.item(i).size;
    if (filetype.includes('image') || filetype.includes('video')) {
      console.log(file_size);
      if (file_size < 20000000) {
        return true;
      } else {
        upload_element.value = "";
        alert("File too huge!");
      }
    } else {
      upload_element.value = "";
      alert("Invalid Media");
    }
  }
}

const createReplyCard = (comment, user: string) => {
  console.log(comment.author.username == user);
  let card: string =
    `<div class="card h-100">`
  if (comment.author.username === user) {
    card += `<div class="dropdown">
        <button class="btn dropdown-toggle" type="button" id="dropdownMenuButton-${comment.reply.id}"
          data-bs-toggle="dropdown" aria-expanded="false">
          ...
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton-${comment.reply.id}">
          <li><button id="delete-post-${comment.reply.id}" data-bs-toggle="modal"
              data-bs-target="#delete-modal-${comment.reply.id}" class="dropdown-item">Delete </button></li>
        </ul>
      </div>

      <div class="modal fade" id="delete-modal-${comment.reply.id}" tabindex="-1"
        aria-labelledby="modal-label-${comment.reply.id}" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="modal-label-${comment.reply.id}">Are you sure?</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Once the answer is deleted, can never be restored. Do you want to continue?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-success" data-bs-dismiss="modal">No, Cancel</button>
              <a type="button" class="btn btn-danger" href="/post/delete_answer/${comment.reply.id}">Yes, Delete
                it</a>
            </div>
          </div>
        </div>
      </div>`
  }

  card += `<div class="container-fluid">
        <div class="card-footer row">
          <div class="col">
            <small> @${comment.author.username} comments:</small>
          </div>
          <div class="col d-flex flex-row-reverse">`
  if (comment.reply.already_voted) {
    card += ` <i class="fas fa-check-circle" id = "answer-${comment.reply.id}" title = "Remove Support"
              onclick="voteAnswer(${comment.reply.id})"></i>`
  } else {
    card += `<i class="fas fa-check" id = "answer-${comment.reply.id}" title = "Support"
  onclick = "voteAnswer(${comment.reply.id})" >
    </i>
  `
  }

  card +=
    `&nbsp; &nbsp; &nbsp;
    <i class="far fa-flag" id = "report-answer-${comment.reply.id}" data-bs-toggle="modal"
  data-bs-target="#report-modal-${comment.reply.id}" onclick = "reportAnswer(${comment.reply.id})" > </i>
      <div class= "modal fade" id = "report-modal-${comment.reply.id}" tabindex="-1" aria-labelledby="modal-label-${comment.reply.id}" aria-hidden="true" >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modal-label-${comment.reply.id}"> Comment was reported!</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                We'll check this post and if it is against our policy, we will remove it. Thank you so much
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"> Okay </button>
                      </div>
                      </div>
                      </div>
                      </div>
                        </div>
                        </div>
                        </div>
                          `;
  const date_obj = new Date(comment.reply.posted_on);
  card += `<div class="card-body">
        <p class="card-text"> ${comment.reply.text} </a></p>
        <small class="text-secondary"> On
          <time datetime="${comment.reply.posted_on}|date:'c'}"
            id="time-${comment.reply.id}">${date_obj.toDateString().toString().slice(4) + " at " + date_obj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</time>
        </small>
        &nbsp; &nbsp; &nbsp;
      </div>`
  return card;
}

const setPageNumber = (answer_id:string,page_number:number,user:string) => {
  const button = document.getElementById(`load-replies-button-${answer_id}`);
  button.setAttribute('onClick', `fetchComment(${answer_id},${page_number},'${user}')`)
}

const fetchComment = async (answer_id: string, page_number: number, user: string) => {
  const response = await makeRequest(`/api/fetch_answer_replies/${answer_id}/${page_number}`);
  const data: JSON = response.data;
  const parent_element: Element = document.getElementById(`load-replies-${answer_id}`);
  if (Object.keys(data).length === 0) {
    const load_button = document.getElementById(`load-replies-button-${answer_id}`);
    load_button.remove();
  } else {
    for (const comment of data) {
    console.log(comment);
    parent_element.insertAdjacentHTML('afterbegin', createReplyCard(comment, user));
  }
  }

  setPageNumber(answer_id,page_number+1,user);
}

document.addEventListener('DOMContentLoaded', () => {
  const elements: NodeList = document.querySelectorAll('time');
  elements.forEach(function (element: Element) {
    const iso_time: string = element.getAttribute("datetime");
    const id: string = element.getAttribute('id');
    convertDateFormat(iso_time, id);
  })
})


