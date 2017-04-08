% import string
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{{siteName}}ランキング</title>
    </head>

    <body>
        <table>
            <thead>
                <tr>
                % for date in dates:
                    <th>{{date}}</th>
                % end
                </tr>
            </thead>
            <tbody>
                % date_length = len(dates)
                % for i in range(10):
                <tr>
                    % for d in range(len(dates)):
                    <!--<td>{{jdata[d][i]['site']}}</td>
                    <td>{{jdata[d][i]['category_id']}}</td>
                    <td>{{jdata[d][i]['category_num']}}</td>
                    <td>{{jdata[d][i]['response']}}</td>
                    <td>{{jdata[d][i]['get_time']}}</td>
                    <td>{{jdata[d][i]['rank']}}</td>
                    <td>{{jdata[d][i]['asin']}}</td>
                    <td>{{jdata[d][i]['url']}}</td>
                    <td>{{jdata[d][i]['title']}}</td>
                    <td>{{jdata[d][i]['brand']}}</td>
                    <td>{{jdata[d][i]['shop']}}</td>
                    <td>{{jdata[d][i]['price']}}</td>
                    <td>{{jdata[d][i]['sales_rank']}}</td>
                    -->
                    <td>{{jdata[d][i]['img_url'].replace('\/', '/')}}</td>
                    <td><img src="data:image/png;base64,{{jdata[d][i]['img_data'].replace('\/', '/')}}" /></td>
                    % end
                </tr>
                % end
            </tbody>
        </table>
    </body>
</html>