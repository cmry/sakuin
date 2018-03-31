
    <ol class="breadcrumb" dir="ltr">
      <li><a href="{{args['base']}}"><i class="fas fa-home"></i></a></li>
      %for dir_d in fils[0].split('/')[:-1]:
      <li>{{dir_d}}</li>
      %end
    </ol>
    <!--
    <div class="row">
      <div class="col-lg-9"></div>
      <div class="col-lg-3">
        <div class="input-group mb-3">
          <div class="input-group-prepend">
            <span class="input-group-text"><i class="fa fa-search form-control-feedback"></i></span>
          </div>
          <input class="form-control" aria-label="search" type="text">
        </div>
      </div>
    </div>
    -->
    <div class="row">
      <div class="table-responsive">
        <table id="bs-table" class="table table-hover">
          <thead>
            <tr>
              <th class="text-right" data-sort="int">#</th>
              <th class="col-sm-8 text-left" data-sort="string">Name</th>
              <th class="col-sm-2 text-right" data-sort="int">Size</th>
              <th class="col-sm-2 text-right" data-sort="int">Modified</th>
            </tr>
          </thead>
          <tfoot>
            <tr>
              <td colspan="4">
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
              <td class="text-right" data-sort-value="{{finf[entry]['bsize']}}">{{finf[entry]['size']}}</td>
              <td class="text-right" data-sort-value="{{finf[entry]['ctime']}}" title="{{finf[entry]['date']}}">{{finf[entry]['date']}}</td>
            </tr>
            %end
          </tbody>
        </table>
    </div>
  </div>
