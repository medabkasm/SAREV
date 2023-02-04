/* globals Chart:false, feather:false */
window.addEventListener('load',function(){

(function () {

  'use strict'

  feather.replace({ 'aria-hidden': 'true' });

  // Graphs
  var ctx = document.getElementById('myChart');
  var chart = document.getElementById("chart");
  var viewChart = document.getElementById("getChart");
  var table = document.getElementById("table");
  var viewBills = document.getElementById("getBills");
  var alert = document.getElementById("alert");
  var viewUsers = document.getElementById("getUsersEmp");
  var usersEmp = document.getElementById("usersEmp");
  var usersEmpTab = document.getElementById("usersEmpTab");
  var usersEmp = document.getElementById("usersEmp");
  var viewBillsEmp = document.getElementById("getBillsEmp");
  var billsEmp = document.getElementById("billsEmp");



  if(search){
    search.disabled = true;
  }
  if(table){
    table.style.display = "none";
  }
  if(chart){
    chart.style.display = "none";
  }
  if(alert){
    alert.style.display = "none";
  }
  if(usersEmp){
    usersEmp.style.display = "none";
  }
  if(billsEmp){
    billsEmp.style.display = "none";
  }

  if(getBillsEmp){
    getBillsEmp.onclick = function(event){
      if(billsEmp.style.display == "none"){
        usersEmp.style.display = "none";
        billsEmp.style.display = "block";
        usersEmpTab.innerHTML = "";
        $.ajax({
              type: "GET",
              url: "/manager/ajax/bills/",
              data: "no data",
              success : function(bills,status,xhr){

                for(var i = 0 ; i < bills['bills'].length ; i++){
                //var user = users['users'][i];
                  var tr = document.createElement("tr");
                  var td = document.createElement("td");
                  const id = document.createTextNode(bills['bills'][i].id);
                  const username = document.createTextNode(bills['bills'][i].username);
                  const power = document.createTextNode(bills['bills'][i].power);
                  const amount = document.createTextNode(bills['bills'][i].amount);
                  const date = document.createTextNode(bills['bills'][i].date);
                  const payed = document.createTextNode(bills['bills'][i].payed);
                  var a = document.createElement("a");
                  a.href = "/manager/user_bill/"+bills['bills'][i].id+"/";
                  a.appendChild(id);
                  td.appendChild(a);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(username);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(power);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(amount);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(date);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(payed);
                  tr.appendChild(td);

                  billsEmpTab.appendChild(tr);
                }

              },
            error : function(xhr,status,data){
              console.log(status);
              }
            });

      }
      else{
        billsEmp.style.display = "none";
        billsEmpTab.innerHTML = "";
      }

    };
  }

  if(getUsersEmp){
    getUsersEmp.onclick = function(event){

      if(usersEmp.style.display == "none"){
        usersEmp.style.display = "block";
        billsEmp.style.display = "none";
        billsEmpTab.innerHTML = "";
        $.ajax({
              type: "GET",
              url: "/manager/ajax/users/",
              data: "no data",
              success : function(users,status,xhr){

                for(var i = 0 ; i < users['users'].length ; i++){
                //var user = users['users'][i];
                  var tr = document.createElement("tr");
                  var td = document.createElement("td");
                  const id = document.createTextNode(users['users'][i].id);
                  const username = document.createTextNode(users['users'][i].username);
                  const email = document.createTextNode(users['users'][i].email);
                  const phone = document.createTextNode(users['users'][i].phone);
                  const joined = document.createTextNode(users['users'][i].joined);
                  const profileComplete = document.createTextNode(users['users'][i].profileComplete);
                  var a = document.createElement("a");
                  a.href = "/manager/user_profile/"+users['users'][i].username+"/";
                  a.appendChild(id);
                  td.appendChild(a);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(username);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(email);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(phone);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(joined);
                  tr.appendChild(td);
                  var td = document.createElement("td");
                  td.appendChild(profileComplete);
                  tr.appendChild(td);
                  usersEmpTab.appendChild(tr);
                }

              },
            error : function(xhr,status,data){
              console.log(status);
              }
            });
      }
      else{
        usersEmp.style.display = "none";
        usersEmpTab.innerHTML = "";
      }
    }
  }

    if(viewBills){
      viewBills.onclick = function(event){
        if(table.style.display == "none"){
          table.style.display = "block";
          chart.style.display = "none";
          alert.style.display = "none";
        }
        else{
          table.style.display = "none";
        }
      };
    }

  if(viewChart){
    viewChart.onclick = function(event){
      if(chart.style.display == "none"){
        chart.style.display = "block";
        table.style.display = "none";
        alert.style.display = "none";
              $.ajax({
                    type: "GET",
                    url: "/manager/ajax/normal_user/chart/",
                    data: "no data",
                    success : function(datas,status,xhr){

                      feather.replace({ 'aria-hidden': 'true' })

                    // Graphs
                    var ctx = document.getElementById('myChart');
                    // eslint-disable-next-line no-unused-vars
                    var myChart = new Chart(ctx, {
                      type: 'line',
                      data: {
                        labels: datas['date'],
                        datasets: [{
                          data: datas['power'],
                          lineTension: 0,
                          backgroundColor: 'transparent',
                          borderColor: '#007bff',
                          borderWidth: 4,
                          pointBackgroundColor: '#000000'
                        }]
                      },
                      options: {
                        scales: {
                          yAxes: [{
                            ticks: {
                              beginAtZero: false
                            }
                          }]
                        },
                        legend: {
                          display: false
                        }
                      }
                    });

                    var ctx2 = document.getElementById('myChart2');
                    // eslint-disable-next-line no-unused-vars
                    var myChart2 = new Chart(ctx2, {
                      type: 'line',
                      data: {
                        labels: datas['date'],
                        datasets: [{
                          data: datas['current'],
                          lineTension: 0,
                          backgroundColor: 'transparent',
                          borderColor: '#cc1919',
                          borderWidth: 4,
                          pointBackgroundColor: '#000000'
                        }]
                      },
                      options: {
                        scales: {
                          yAxes: [{
                            ticks: {
                              beginAtZero: false
                            }
                          }]
                        },
                        legend: {
                          display: false
                        }
                      }
                    });



                    },
                    error : function(xhr,status,data){
                      chart.style.display = "none";
                      alert.style.display = "block";
                    }
                  });

      }
      else{
        chart.style.display = "none";
      }

    };
  }
  // eslint-disable-next-line no-unused-vars

})()

},true);
