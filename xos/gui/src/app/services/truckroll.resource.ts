export class XosVtrTruckroll {

  static $inject = [
    '$resource',
    'AppConfig'
  ];

  constructor(
    private $resource: ng.resource.IResourceService,
    private AppConfig: any
  ) {

  }

  public getResource() {
    return this.$resource(`${this.AppConfig.apiEndpoint}/vtr/vtrtenants/:id/`, { id: '@id' }, {
      update: { method: 'PUT' }
    });
  }
}
