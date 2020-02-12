var form = document.getElementById('form');
var options = [ '1', '2', '3', '4' ];
options.forEach(function(element, key) {
  if (element == '1') {
    form[form.options.length] = new Option(element, form.options.length, true, false);
  }
  if (element == '2') {
    form[form.options.length] = new Option(element, form.options.length, true, false); // Will add the "selected" attribute    
  }
  if (element == '3') {
    form[form.options.length] = new Option(element, form.options.length, true, false); // Just will be selected in "view"
  }
  if (element == '4') {
    form[form.options.length] = new Option(element, form.options.length, true, false); // Just will be selected in "view"
  }
});