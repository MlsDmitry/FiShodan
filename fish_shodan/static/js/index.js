// import axios 

// const axios = require('axios').default;

const btn = document.getElementById('submit-btn')
const form = document.getElementById('main_form');

async function sendForm(ips) {

  let r = await fetch('/tasks', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          'domains': JSON.stringify(ips)
      }),
  })
  .then(response => response.json())
  .then(data => {
      console.log('Success:', data);
      getStatus(data.task_ids)
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
      
      var ips = []
      if (inpDomain != "") {
        ips.push(inpDomain)
      }
      if (inpFile.files.length) {
        var reader = new FileReader()
        var data = reader.readAsText(inpFile.files[0])
        console.log(data)
        data.split("\n").forEach((el) => {
          ips.push(el)
        })
      }
      sendForm(ips)
  }
}

async function okey(resp) {
  var data = await resp
  var task_ids = []
  for (var key in data) {
    insertData(data[key])
    if (data[key]["task_status"] != "SUCCESS") {
      task_ids.push(key)
    }
  }

  setTimeout(function() {

    getStatus(task_ids);
  }, 5000);
}

function insertData(results) {
  var list = document.getElementsByClassName("list__tasks")[0];
  // var res = JSON.parse(results);
  var htmlCode = "";

  
  htmlCode += `<div class="task">
      <div class="task__header">
          Id таска: ${ results["task_id"] }
      </div>
      <div class="task__status">
          Статус: ${ results["task_status"] }
      </div>
      <div class="task__result">
          Результат: ${ results["task_result"] }
      </div>
  </div>`

  list.innerHTML += htmlCode
  
}


function getStatus(taskIDs) {
  console.log("Task ids are: " + taskIDs.join(';'))
    fetch(`/tasks/${taskIDs.join(';')}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })
    .then(response => okey(response.json()))
    .catch(err => console.log(err));
}