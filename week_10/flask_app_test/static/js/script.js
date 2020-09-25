// sanity check
//console.log('Everything is linked and working');
var button = document.getElementsByClassName('submit-button-container')[0];
//console.log(button);
button.addEventListener('mouseover', function(){
  console.log('hello from mr. Button!')
  button.style.background = 'blue';
});
button.addEventListener('mouseout', function(){
  console.log('goodbye!')
  button.style.background = 'red';
});
