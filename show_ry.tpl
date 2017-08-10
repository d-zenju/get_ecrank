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
    <h3>{{siteName}}ランキング {{rows[0][0][3]}} ({{rows[0][0][4]}})</h3>
    <table class="rank-table">
        <thead>
            <tr>
                <th>Rank</th>
                % for date in dates:
                    <th>{{date}}</th>
                % end
            </th>
        </thead>
        <tbody>
        % for i in range(10):
            <tr>
                <th>{{i+1}}</th>
                % for d in range(len(dates)):
                    <td>
                        <div class="title"><a href="{{rows[d][i][8]}}">{{rows[d][i][9]}}</a></div>
                        <div class="cbr"></div>
                        <a href="{{rows[d][i][8]}}"><img src="{{rows[d][i][13]}}" class="left"></a>
                        <div class="casin">{{rows[d][i][7]}}</div>
                        <div class="cbr"></div>
                        <a href="{{rows[d][i][11]}}"><div class="cshopname">{{rows[d][i][10]}}</div></a>
                        <div class="cbr"></div>
                        <div class="cprice">¥{{rows[d][i][12]}}</div>
                    </td>
                % end
            </tr>
        % end
        </tbody>
    </table>
</body>
</html>