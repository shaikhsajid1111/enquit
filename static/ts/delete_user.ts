const match = () => {
  const text = (Math.random() + 1).toString(36).substring(7);
  const element = document.querySelector("#re-check");
  element.setAttribute('value', text);
}

const match_values = () => {
  const element = document.getElementById('re-check');
  const element2 = document.getElementById('re-check-2');
  if (element.value === element2.value) {
    document.getElementById('delete-account').classList.remove('disabled');
  }
}