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
      manipulate(`vote-${answer_id}`, 'Un-Vote');
      updateVoteCount(`vote-count-${answer_id}`, true);
    } else {
      manipulate(`vote-${answer_id}`, 'Vote');
      updateVoteCount(`vote-count-${answer_id}`, false);

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
  const time_string:string = date_obj.toDateString().toString().slice(4) + " at " + date_obj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  document.getElementById(id).innerHTML = time_string.toString();
}

function Validate() {
  const upload_element = document.getElementById("upload");
  for (let i = 0; i < upload_element.files.length; i++){
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

document.addEventListener('DOMContentLoaded', () => {
  const elements: NodeList = document.querySelectorAll('time');
  elements.forEach(function (element: Element) {
    const iso_time: string = element.getAttribute("datetime");
    const id: string = element.getAttribute('id');
    convertDateFormat(iso_time, id);
  })
})


