window.addEventListener('load', () => {
    // 로고 클릭시 홈화면으로 이동
    document.getElementById('plyyLogo').addEventListener('click', () => {
        location.href = '/';
    })
    // 프로필 아이콘 클릭시 로그인 페이지로 이동
    document.getElementById('myProfile2').addEventListener('click', () => {
        location.href = '/login';
    })
    // 플로팅바 : 뒤로가기 
    document.getElementById('historyBack').addEventListener('click', ()=>{
        window.history.back();
    })
})

