# vTR GUI

This GUI provide the interface to perform a vTR test.

## Platform install integration

Having a profile deployed is required. To add extensions listed in your `profile-manifest` as:

```
enabled_gui_extensions:
  - name: vtr
    path: orchestration/xos_services/vtr/xos/gui
```

Execute: `ansible-playbook -i inventory/mock-rcord deploy-xos-gui-extensions-playbook.yml`
_NOTE: remember to replate `inventory/**` with the actual `cord_profile` you are using_ 