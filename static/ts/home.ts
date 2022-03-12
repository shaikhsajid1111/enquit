/**
 * @author Akankshi Gupta <akankshigp12345@gmail.com>
 */
const makeRequest = async (url: string) => {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    console.log(`Error at makeRequest:  ${error.message}`);
    return null;
  }

}

const manipulate = (id:string, value:string) => {
  document.getElementById(id).innerHTML = value;
}

const updateVoteCount = (id:string, upvote:boolean) => {
  if (upvote) {
    const vote_count_element = document.getElementById(id);
    const increment_count = parseInt(vote_count_element.innerHTML) + 1;
    vote_count_element.innerHTML = increment_count.toString();
  } else {
    const vote_count_element = document.getElementById(id);
    const increment_count = parseInt(vote_count_element.innerHTML) - 1;
    vote_count_element.innerHTML = increment_count.toString();
  }
}

const toggleIcon = (id:string,icon_class_to_add:string,icon_class_to_remove:string) => {
  try {
    const element = document.getElementById(id);
    element.classList.remove(icon_class_to_remove);
    element.classList.add(icon_class_to_add);

  } catch (error) {
    console.error('Error at ToggleIcon  : ', error.message);
  }
}

const votePost = async (post_id:number) => {
  try {
    const url = `/api/vote_post/${post_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Voted the post!') {
      toggleIcon(`vote-${post_id}`,'fa-check-circle','fa-check');
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
    const url = `/api/vote_answer/${answer_id}`;
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

const updateSavedButton = (state:boolean,post_id:number) => {
  /**if the state is true means a new post was saved */
  const element_id = `saved-${post_id}`;
  const element = document.getElementById(element_id);
  if (state == true) {
    element.innerHTML = 'Save';
  } else if(state == false) {
    /**else if the state is false, post have been unsaved */
    element.innerHTML = 'Unsave';
  }
}

const savePost = async (post_id: number) => {
  try {
    const url = `/api/save/${post_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Unsaved the answer!') {
      toggleIcon(`saved-${post_id}`,'far','fas');
    } else {
      toggleIcon(`saved-${post_id}`, 'fas', 'far');
    }
  } catch (error) {
    console.warn(error.message);
  }
}


const reportPost = async (post_id: number) => {
  try {
    const url = `/api/report_post/${post_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Reported!') {
      toggleIcon(`report-post-${post_id}`,'fas','far');
    }
  } catch (error) {
    console.error(`Error at Report Post : ${error.message}`);
  }
}

const reportAccount = async (account_id: number) => {
  try {
    const url = `/api/report_account/${account_id}`;
    const response = await makeRequest(url);
    if (response.message == 'Reported!') {
      toggleIcon(`report-account-${account_id}`, 'fas', 'far');
    }
  } catch (error) {
    console.error(`Error at Report Account : ${error.message}`);
  }
}