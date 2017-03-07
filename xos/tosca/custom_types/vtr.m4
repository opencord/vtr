tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 vtr.m4 > vtr.yaml"

# include macros
include(macros.m4)

node_types:
    tosca.nodes.VTRService:
        derived_from: tosca.nodes.Root
        description: >
            VTR Service
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            xos_base_service_props

