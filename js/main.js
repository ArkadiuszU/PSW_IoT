const url_for_latest_message='https://dweet.io/get/latest/dweet/for/au';
const url_for__messages='https://dweet.io/get/dweets/for/au';

const pull_data_to_view = (response) =>
{

  let parts = response.created.split("T");
  date_time= `${parts[0]} ${parts[1].slice(0,8)}`
  data = response.content;
  const infos1 = document.querySelector(".infos1")
  const infos2 = document.querySelector(".infos2")
  const img =  document.querySelectorAll("img")
  const temps = document.querySelector(".temps")

  infos1.querySelector("#actual_bath_time").innerText = data.actual_bath_time;
  infos1.querySelector("#actual_bath_name").innerText = data.actual_bath_name;
  infos2.querySelector("#counter").innerText = data.total_bath_counter;
  infos2.querySelector("#status").innerText = data.status;
  switch(data.status)
  {
    case "ok" :
      img[4].style.backgroundColor = "green";
      break;
    case "work" :
      img[4].style.backgroundColor = "yellow";
      break;
    case "fault" :
      img[4].style.backgroundColor = "red";
      break;
  }
  infos1.querySelector("#data").innerHTML = date_time;
  temps.querySelector("#developer").innerText = data.temp[0];
  temps.querySelector("#stop_bath").innerText = data.temp[1];
  temps.querySelector("#fixer").innerText = data.temp[2];
}


API_wait = false; 

function get_latest_message(){
     API_wait = true;
    fetch(url_for_latest_message).then(function(response) {
      response.json().then(function(parsedJson) {

        if(parsedJson.this == "failed")
        {
          console.log("failed")
        }
        
        else{
          console.log("succeeded")
          pull_data_to_view(parsedJson.with[0])
        }

        API_wait = false;

      }
      )
    })
  }

   window.setInterval(() =>{

    if(!API_wait)
    {

      get_latest_message();
    }

   }, 1500);