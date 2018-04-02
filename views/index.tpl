      %try:
      <a class="col-md-2 breadcrumb pull-right text-muted" href="{{'/logout'}}" title="Logout" target="_blank">Logout • {{args['aaa'].current_user.username}}</a>
      %except:
      <a class="col-md-2 breadcrumb pull-right text-muted" href="{{'/login'}}" title="Login" target="_blank">Login</a>
      %end
      <ol class="col-md-10 breadcrumb">
        <li><a href="{{args['base']}}"><i class="fas fa-home"></i></a></li>
        %for dir_d in fils[0].split('/')[:-1]:
        <li>{{dir_d}}</li>
        %end
      </ol>


    <div class="row">
      <div class="table-responsive">
        <table id="bs-table" class="table table-hover">
          <thead>
            <tr>
              <th class="text-right" data-sort="int">#</th>
              <th class="col-sm-3 text-left" data-sort="string">Name</th>
              <th class="col-sm-6 text-left" data-sort="string">Meta</th>
              <th class="col-sm-1 text-right" data-sort="int">Size</th>
              <th class="col-sm-2 text-right" data-sort="int">Modified</th>
            </tr>
          </thead>
          <tfoot>
            <tr>
              <td colspan="5">
                <small class="pull-left text-muted" dir="ltr">{{fsum['dcount']}} directories and {{fsum['fcount']}} files, {{fsum['size']}} in total</small>
                <a class="pull-right small text-muted" href="https://github.com/cmry/sakuin" title="Bootstrap Listr on GitHub" target="_blank">Source on GitHub</a>
              </td>
            </tr>
          </tfoot>
          <tbody>
            %for i, entry in enumerate(dirs):
            <tr style="background-color: inherit;">
              <td class="text-muted text-right" data-sort-value="{{i + 1}}">{{i + 1}}</td>
              <td class="text-left" data-sort-value="checksum">
                <i class="fa fa-folder"></i>&nbsp;
                <a href="{{args['base'] + entry}}"><strong>{{entry}}</strong></a>
              </td>
              <td></td>
              <td class="text-right" data-sort-value="{{finf[entry]['bsize']}}">{{finf[entry]['size']}}</td>
              <td class="text-right" data-sort-value="{{finf[entry]['ctime']}}" title="{{finf[entry]['date']}}">{{finf[entry]['date']}}</td>
            </tr>
            %end
            %for j, entry in enumerate(fils):
            <tr style="background-color: inherit;">
              <td class="text-muted text-right" data-sort-value="{{len(dirs) + j + 2}}">{{len(dirs) + j + 1}}</td>
              <td class="text-left" data-sort-value="checksum">
                %if '.py' in entry:
                <i class="fab fa-python"></i>&nbsp;
                %elif '.csv' in entry:
                <i class="fas fa-table"></i>&nbsp;
                %elif '.json' in entry:
                <i class="fab fa-js"></i>&nbsp;
                %else:
                <i class="fas fa-file"></i>&nbsp;
                %end
                <a href="{{args['base'] + '_public/' + entry}}"><strong>{{entry.split('/')[-1]}}</strong></a>
              </td>
              %if finf[entry]['meta']:
                <td>
                %for k, v in finf[entry]['meta'].items():
                  %if k == 'name':
                  <div class="col-sm-12 pull-right">{{v}} <br>&nbsp;</div>
                  %elif k == 'source_name':
                  <div class="col-sm-6 pull-right"><b>source</b>: <a href="{{finf[entry]['meta']['source_url']}}">{{v}}</a></div>
                  %elif k == 'source_url':
                  %pass
                  %else:
                  <div class="col-sm-6 pull-right"><b>{{k}}</b>: {{v}}</div>
                  %end
                %end
                </td>
              %else:
              <td></td>
              %end
              <td class="text-right" data-sort-value="{{finf[entry]['bsize']}}">{{finf[entry]['size']}}</td>
              <td class="text-right" data-sort-value="{{finf[entry]['ctime']}}" title="{{finf[entry]['date']}}">{{finf[entry]['date']}}</td>
            </tr>
            %end
          </tbody>
        </table>
    </div>
  </div>
