
/*
 * Copyright 2017-present Open Networking Foundation

 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at

 * http://www.apache.org/licenses/LICENSE-2.0

 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


/// <reference path="../typings/index.d.ts" />
import * as angular from 'angular';

import 'angular-ui-router';
import 'angular-resource';
import 'angular-cookies';
import {xosVtrDashboardComponent} from './app/components/vtr/vtr-dashboard';
import {XosVtrTruckroll} from './app/services/truckroll.resource';

angular.module('xos-vtr-gui-extension', [
    'ui.router',
    'app'
  ])
  .service('XosVtrTruckroll', XosVtrTruckroll)
  .component('xosVtrDashboardComponent', xosVtrDashboardComponent)
  .run(function($log: ng.ILogService, XosNavigationService: any, XosRuntimeStates: any) {
    $log.info('[xos-vtr-gui-extension] App is running');

    XosNavigationService.add({
      label: 'Vtr',
      state: 'xos.vtr',
    });

    XosNavigationService.add({
      label: 'Dashboard',
      state: 'xos.vtr.dashboard',
      parent: 'xos.vtr'
    });

    XosRuntimeStates.addState(`xos.vtr`, {
      abstract: true,
      template: '<div ui-view></div>'
    });

    XosRuntimeStates.addState(`xos.vtr.dashboard`, {
      url: 'vtr/dashboard',
      parent: 'xos.vtr',
      component: 'xosVtrDashboardComponent'
    });
  });
