<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{siteName}}ランキング}}</title>
    <style type="text/css">
        img.left {
            float: left;
            max-width: 150px;
            max-height: 150px;
            height: auto;
        }
        .rank-table {
            
            border-collapse: collapse;
            border: 1px #1C79C6 solid;
        }
        .rank-table th {
            border: 1px #1C79C6 solid;
            padding: 0px;
        }
        .rank-table td {
            border: 1px #1C79C6 solid;
            padding: 0px;
        }
        .cbr { margin-bottom:0.5em; }
        .title {
            overflow: hidden;
            width: 100%;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 3;
        }
        .casin {
            text-align: center;
            font-size: 50%;
            color: #111111;
        }
        .cshopname {
            text-align: center;
            overflow: hidden;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 2;
        }
        .csalesrank {
            text-align: center;
        }
        .cprice {
            text-align: center;
            font-size: 120%;
            color: #ff0000;
        }
    </style>
</head>

<body>
    <h3>{{siteName}} ランキング</h3>
    % for row in rows:
        <p>0: {{row[0]}}</p>
        <p>1: {{row[1]}}</p>
        <p>2: {{row[2]}}</p>
        <p>3: {{row[3]}}</p>
        <p>4: {{row[4]}}</p>
        <p>5: {{row[5]}}</p>
        <p>6: {{row[6]}}</p>
        <p>7: {{row[7]}}</p>
        <p>8: {{row[8]}}</p>
        <p>9: {{row[9]}}</p>
        <p>10: {{row[10]}}</p>
        <p>11: {{row[11]}}</p>
        <p>12: {{row[12]}}</p>
        <p>13: {{row[13]}}</p>
        <img src="data:image/png;base64,{{row[14]}}" class="left">
    % end
</body>
</html>