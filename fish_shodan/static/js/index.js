const btn = document.getElementById('btn__submit')
const form = document.getElementById('main_form');

async function sendForm() {
    const fd = new FormData(form)
    console.log(JSON.stringify(Object.fromEntries(fd)))
    let r = await fetch('/tasks/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
        // body: JSON.stringify({
        //     'single_domain': 'example.com'
        // }),
    })
    // .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        getStatus(data.data.task_id)
    })
    .catch((error) => {
        console.log('Error: ', error)
    })
}

function getData() {
  var inpDomain = document.getElementById("input__domain");
  var inpFile = document.getElementById("input__file");
  if (inpDomain.value === "" && inpFile.value === "") {
      console.log(inpDomain.value);
      inpDomain.classList.add("warning"); 
      console.log(inpFile.value);
  } else {
      inpDomain.classList.remove("warning");  
      sendForm();
      window.location.replace("./tasks/index.html");
  }
}

function getStatus(taskID) {
    fetch(`/tasks/${taskID}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then(response => okey())
    .then(res => {
        console.log(res.data)
      setTimeout(function() {
        getStatus(res.data.task_id);
      }, 1000);
    })
    .catch(err => console.log(err));
  }