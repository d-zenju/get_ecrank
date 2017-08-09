<!doctype html>
<html lang="jp">

<head>
    <meta charset="utf-8">
    <title>楽天市場 ECランキング</title>

    <script type="text/javascript">
    <!--
    function functionName()
    {
        var select1 = document.forms.formName.selectName1; //変数select1を宣言
        var select2 = document.forms.formName.selectName2; //変数select2を宣言
         
        select2.options.length = 0; // 選択肢の数がそれぞれに異なる場合、これが重要
        
        % for category in categories:
        if (select1.options[select1.selectedIndex].value == "{{category}}")
        {
            <% i = 0 %>
            % for date in dates:
                % if date[0] == category:
                    select2.options[{{i}}] = new Option("{{date[1]}}", "{{date[2]}}");
                    <% i += 1 %>
                % end
            % end
        }
        % end
    }
    -->
    </script> 
</head>

<body onLoad="functionName()">
    <h3>楽天市場ランキング</h3>
    <form name="formName" method="post" action="./pathToProgramFile">
    <p><!--選択肢その1-->
    <select name = "selectName1" onChange="functionName()">
        % for category in categories:
        <option value = "{{category}}">{{category}}</option>
        % end
    </select></p>
    <p><!--選択肢その2（選択肢その1の項目によって変化）-->
    <select name = "selectName2" size = "24" multiple>
    </select></p>
    <input type="hidden" name = "楽天市場" value = "rakuten">
    <p>
    <input type="submit" value="送信">
    </p>
    </form>
</body>


</html>