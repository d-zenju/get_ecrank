<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{siteName}}ランキング</title>
    <style type="text/css">
        img.left {
            float: left;
            max-width: 100px;
            height: auto;
        }
        .rank-table {
            width: 900px;
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
    </style>
</head>

<body>
    <h3>{{siteName}} ランキング</h3>
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
                            <p>{{jdata[d][i]['title']}}</p>
                            <img src="data:image/png;base64,{{jdata[d][i]['img_data']}}" class="left">
                            <p>{{jdata[d][i]['shop']}}</p>
                            <p>{{jdata[d][i]['sales_rank']}}</p>
                            <p>{{jdata[d][i]['price']}}</p>
                        </td>
                    % end
                </tr>
            % end
        </tbody>
    </table>
</body>
</html>