let updateBtn = document.getElementsByClassName('update-cart')

for(i=0; i < updateBtn.length; i++){
    updateBtn[i].addEventListener('click',function (){
      
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('Product Id:',productId,'Action:',action)
        console.log(user)
        if(user == 'AnonymousUser'){
            console.log('user is not logged in...')
        }else{
            updateorder(productId,action);
        }
    })
}
function updateorder(productId,action){

    let url ='/update_item/'

    fetch(url,{
        method:'POST',
        headers:{
           'Content-Type': 'application/json',
           'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then(response => {
        return response.json();
    })
    .then(data =>{
        console.log('data',data)
        location.reload();
    })
}

let updateCustomBtn = document.getElementsByClassName('update-custom')

for(i=0; i < updateCustomBtn.length; i++){
    updateCustomBtn[i].addEventListener('click',function (){
      
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('Product Id:',productId,'Action:',action)
        console.log(user)
        if(user == 'AnonymousUser'){
            console.log('user is not logged in...')
        }else{
            updatecustomorder(productId,action);
        }
    })
}
function updatecustomorder(productId,action){

    let url ='/update_custom_item/'

    fetch(url,{
        method:'POST',
        headers:{
           'Content-Type': 'application/json',
           'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then(response => {
        return response.json();
    })
    .then(data =>{
        console.log('data',data)
        location.reload();
    })
}
