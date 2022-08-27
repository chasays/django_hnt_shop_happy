// const data = [
//     { text: 'Slide 1', color: 'primary' },
//     { text: 'Slide 2', color: 'info' },
//     { text: 'Slide 3', color: 'success' },
//     { text: 'Slide 4', color: 'warning' },
//     { text: 'Slide 5', color: 'danger' }
// ]
console.log('asdas')
var banner = new Vue({
    el: '#banner',
    delimiters: ['{$', '$}'],
    data:{
        // carousels: data
        carousels: []
    },
    created(){
        console.log(this.carousels)
        request({
            url: '/banners/',
            method: 'get'
        }).then(res => {
            this.carousels = res
        })
    }

})