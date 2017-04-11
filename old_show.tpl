% import string
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{{siteName}}ランキング</title>
        <link rel="stylesheet" href="css/show.css">
    </head>

    <body>
       <div class="post clearfix">
  <div class="thumbnail">
    <img src="https://s3-ap-southeast-1.amazonaws.com/nulab-blog/wp-content/uploads/sites/2/2016/04/nulab-120x120.jpg" alt="nulab" />
  </div>
  <div class="media">
    <p class="title">nulab</p>
    <p class="subtitle">nulabは仕事上のコミュニケーションやコラボレーションを
促進するサービスを開発しています。</p>
  </div>
</div>
    </body>
</html>


    <!--
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    % for date in dates:
                        <th>{{date}}</th>
                    % end
                </tr>
            </thead>
            <tbody>
                % for i in range(10):
                <tr>
                    <td rowspan="2">{{i+1}}</td>
                    % for d in range(len(dates)):
                    <td colspan="2">{{jdata[d][i]['title']}}</td>

                    <td>{{jdata[d][i]['site']}}</td>
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
                    <td>{{jdata[d][i]['img_url']}}</td>
                    <td><img src="data:image/png;base64,{{jdata[d][i]['img_data']}}" /></td>
                    % end
                </tr>
                % end
            </tbody>
        </table>
        -->