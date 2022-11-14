
  var getData = [];
  var usersList = [];

function status(response) {
  //Check Promise
  if (response.status >= 200 && response.status < 300) {
    return Promise.resolve(response)
  } else {
    return Promise.reject(new Error(response.statusText))
  }
}

function json(response) {
  //Return JSON format
  return response.json()
}

function getUsers(){

  fetch('https://jsonplaceholder.typicode.com/users')
  .then(status)
  .then(json)
  .then(function(dataList) {
    usersList = dataList;
    dataList.forEach(function(data){
      $('#selUser').append($('<option>', {
        value: data.id,
        text : data.name
    }));

    });
    getPosts("");


  })
  .catch(function(error) {
    console.log('Fetch User Error :-S', error);
  });

}

function getPosts(option){

  fetch('https://jsonplaceholder.typicode.com/posts' + option)
  .then(status)
  .then(json)
  .then(function(dataList) {
    getData = dataList;
    var divReply = $(".reply")
    divReply.empty();

    dataList.forEach(function(data){
      var post = $('<p class="post"/>');

      var divID = $('<div class="userName"/>').append($('<span>').append('By: ', usersList[data.userId - 1].name));
      var divTitle = $('<div class="title"/>').append(data.title);
      var divBody = $('<div class="body"/>').append(data.body)

      divReply.append(post.append(divID,divTitle,divBody));

    });

  })
  .catch(function(error) {
    console.log('Fetch Post Error :-S', error);
  });
}



$(document).ready(function() {
  //Get Post On Document Ready
  getUsers();
})

function searchUser(){
  var userSelected = $('#selUser').val();

  if (userSelected != 0){
    getPosts("?userId=" + userSelected);
  }
  else{
    getPosts("");
  }
}