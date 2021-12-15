//글쓰기 폼 유효성 검사(테이블 생성 시 not null이라고 명시는 했지만 웹에서 작성 시 입력을 하지 않아도 넘어
function checkWriting(){
    var form = document.writeForm; //폼 선택
    var title = form.title.value; //입력받은 글제목 값
    var content = form.content.value; //입력받은 글내용 값

    if(title == ""){ //글제목 미 입력 시
        alert("제목은 필수 항목입니다");
        form.title.focus(); //오류 시 커서를 해당 위치로 보냄
        return false;
        }
    else if(content == ""){ //글내용 미 입력 시
        alert("내용은 필수 항목입니다");
        form.content.focus();
        return false;
        }
    else{
        form.submit(); //오류가 안 나면 폼 전송
    }
}