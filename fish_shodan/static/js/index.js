// import axios 

// const axios = require('axios').default;

const btn = document.getElementById('submit-btn')
const form = document.getElementById('main_form');

async function sendForm() {
  // const fd = new FormData(form)
  
  // axios.post('/tasks', {
  //     method: 'POST',
  //     data: {
  //         'domain_single': 'example.com',
  //     }
  //   })
  //   .then(function (response) {
  //     console.log(response);
  //   })
  //   .catch(function (error) {
  //     console.log(error);
  //   });

  let r = await fetch('/tasks', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
      // body: JSON.stringify({
      //     'single_domain': 'example.com'
      // }),
  })
  .then(response => response.json())
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
      const fileList = inpFile.files[0];
      console.log(fileList);  
      
      sendForm();
  }
}

function okey() {
  console.log("aaaaaaa")
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