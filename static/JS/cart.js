let updateBtns = document.getElementsByClassName('update-cart')
for (i=0;i<updateBtns.length;i++) {
    updateBtns[i].addEventListener('click', function(){
        let productID = this.dataset.product;
        let action= this.dataset.action;
        console.log('productId: ', productID, 'action ', action)
        console.log("User: ", user)
        if(user==="ANONYMOUS")
        {
            console.log("Not logged in")
        }
        else{
            updateUserOrder(productID, action)
        }
    })
}

function updateUserOrder(productID, action){
    console.log("User is logged in, sending data...");
    var url = "/update_item"
    fetch(url{
        method:"POST",
        headers:{
            'Content-type':'application/json'
        },
        body:JSON.stringify({'productID': productID,'action':action})

        .then((response)=>{
            return response.json();
        })
        .then((data)=>{
            console.log('data: ',data)
        })
    })
}