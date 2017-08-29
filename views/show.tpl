<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{siteName}}ランキング {{jdata[0][0]['category_id']}}</title>
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
    <h3>{{siteName}} 週別売上カテゴリランキング ({{category_name[jdata[0][0]['category_id']]}})</h3>
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
                            <div class="title"><a href="{{jdata[d][i]['url']}}">{{jdata[d][i]['title']}}</a></div>
                            <div class="cbr"></div>
                            <a href="{{jdata[d][i]['url']}}"><img src="data:image/png;base64,{{jdata[d][i]['img_data']}}" class="left"></a>
                            <div class="casin">{{jdata[d][i]['asin']}}</div>
                            <div class="cbr"></div>
                            <div class="cshopname">{{jdata[d][i]['shop']}}</div>
                            <div class="cbr"></div>
                            <div class="csalesrank">SR: {{jdata[d][i]['sales_rank']}}位</div>
                            <div class="cprice">¥{{jdata[d][i]['price']}}</div>
                        </td>
                    % end
                </tr>
            % end
        </tbody>
    </table>
</body>
</html>