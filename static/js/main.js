// Materialize Initializations
$(document).ready(function(){
    // Needed for materialize autocomplete
    $('input.autocomplete').autocomplete({
      data: {
        "Apple": null,
        "Microsoft": null,
        "Google": 'https://placehold.it/250x250'
      },
    });

    // Initialize material box
    $('.materialboxed').materialbox();

    // Initialize sidenav on small screen sizes
    $('.sidenav').sidenav();

    // Initialize select element
    $('select').formSelect();
    
  });

// Functions used on createrecipe.html and editrecipe.html
function addIngredient(){
    let i = parseInt($(".ingredient:last").attr('id').slice(10))
    if(i == 1){
      i++
      $(`<div class="input-field col s3 ingredient${i}">
            <input id="ingredient${i}" name="ingredient${i}" type="text" class="validate ingredient">
          </div>`).insertAfter(`.ingredient${i-1}`)
      $('<a class="btn-floating waves-effect waves-light red" onclick="removeLastIngredient()"><i class="material-icons">delete</i></a>').insertAfter("a[onclick='addIngredient()']")
    } else{
      i++
      $(`<div class="input-field col s3 ingredient${i}">
            <input id="ingredient${i}" name="ingredient${i}" type="text" class="validate ingredient">
          </div>`).insertAfter(`.ingredient${i-1}`)
    }
}

function removeLastIngredient(){
    let i = parseInt($(".ingredient:last").attr('id').slice(10))
    if(i == 2){
      $(`.ingredient${i}`).remove()
      $("a[onclick='removeLastIngredient()']").remove()
    } else{
      $(`.ingredient${i}`).remove()
    }
}

function addTool(){
    let i = parseInt($(".cooking_tool:last").attr('id').slice(12))
    if(i == 1){
      i++
      $(`<div class="input-field col s3 cooking_tool${i}">
            <input id="cooking_tool${i}" name="cooking_tool${i}" type="text" class="validate cooking_tool">
          </div>`).insertAfter(`.cooking_tool${i-1}`)
      $('<a class="btn-floating waves-effect waves-light red" onclick="removeLastTool()"><i class="material-icons">delete</i></a>').insertAfter("a[onclick='addTool()']")
    } else{
      i++
      $(`<div class="input-field col s3 cooking_tool${i}">
            <input id="cooking_tool${i}" name="cooking_tool${i}" type="text" class="validate cooking_tool">
          </div>`).insertAfter(`.cooking_tool${i-1}`)
      }
}

function removeLastTool(){
    let i = parseInt($(".cooking_tool:last").attr('id').slice(12))
    if(i == 2){
      $(`.cooking_tool${i}`).remove()
      $("a[onclick='removeLastTool()']").remove()
    } else{
      $(`.cooking_tool${i}`).remove()
    }
}

function addStep(){
    let i = parseInt($(".prefix:last").html())
    if(i == 1){
      i++
      $(`<div class="input-field col s12 step${i}"><span class="prefix">${i}</span><input id="step${i}" name="step${i}" type="text" class="validate"></div>`).insertAfter(`.step${i-1}`)
      $('<a class="btn-floating btn-large waves-effect waves-light red" onclick="removeLastStep()"><i class="material-icons">delete</i></a>').insertAfter("a[onclick='addStep()']")
    } else{
      i++
      $(`<div class="input-field col s12 step${i}"><span class="prefix">${i}</span><input id="step${i}" name="step${i}" type="text" class="validate"></div>`).insertAfter(`.step${i-1}`)
    }
}

function removeLastStep(){
    let i = parseInt($(".prefix:last").html())
    if(i == 2){
        $(`.step${i}`).remove()
        $("a[onclick='removeLastStep()']").remove()
    } else{
        $(`.step${i}`).remove()
    }
}