from d3m import index
from d3m.metadata.base import ArgumentType
from d3m.metadata.pipeline import Pipeline, PrimitiveStep


# Creating pipeline
pipeline_description = Pipeline()
pipeline_description.add_input(name='inputs')

# Step 0: dataset_to_dataframe
primitive_0 = index.get_primitive('d3m.primitives.tods.data_processing.dataset_to_dataframe')
step_0 = PrimitiveStep(primitive=primitive_0)
step_0.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='inputs.0')
step_0.add_output('produce')
pipeline_description.add_step(step_0)

# Step 1: column_parser
step_1 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.tods.data_processing.column_parser'))
step_1.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.0.produce')
step_1.add_output('produce')
pipeline_description.add_step(step_1)

# Step 2: extract_columns_by_semantic_types(attributes)
step_2 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.tods.data_processing.extract_columns_by_semantic_types'))
step_2.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.1.produce')
step_2.add_output('produce')
step_2.add_hyperparameter(name='semantic_types', argument_type=ArgumentType.VALUE,
                                  data=['https://metadata.datadrivendiscovery.org/types/Attribute'])
pipeline_description.add_step(step_2)

# Step 3: holt smoothing
step_3 = PrimitiveStep(primitive=index.get_primitive('d3m.primitives.tods.timeseries_processing.holt_smoothing'))
step_3.add_argument(name='inputs', argument_type=ArgumentType.CONTAINER, data_reference='steps.2.produce')
step_3.add_hyperparameter(name="exclude_columns", argument_type=ArgumentType.VALUE, data = (2, 3))
step_3.add_hyperparameter(name="use_semantic_types", argument_type=ArgumentType.VALUE, data = True)
step_3.add_output('produce')
pipeline_description.add_step(step_3)

# Final Output
pipeline_description.add_output(name='output predictions', data_reference='steps.3.produce')

# Output to JSON
data = pipeline_description.to_json()
with open('example_pipeline.json', 'w') as f:
    f.write(data)
    print(data)

