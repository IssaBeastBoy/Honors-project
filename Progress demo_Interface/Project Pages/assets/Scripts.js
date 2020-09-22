function openmodal(popup){
    if (popup == null) return
    popup.classList.add('active')
    document.write('see')
}
var popup = document.getElementById('Wrong_file')

if(!window.dash_clientside) {window.dash_clientside = {};}
window.dash_clientside.clientside = {
    display: function openmodal(){
        //if (popup == null) return "Drag and drop"
        return popup.classList.add('active')
        document.write('see')
    }
}