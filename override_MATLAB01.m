function risk_level = xgb_predict_new(input_vector)
    % Load necessary Python packages
    joblib = py.importlib.import_module('joblib');
    np = py.importlib.import_module('numpy');

    % Load XGBoost model (only once)
    persistent model
    if isempty(model)
        model_path= 'E:\Intern-LeSo\Simulink-Files\xgb_risk_model2.pkl';
        model = joblib.load(model_path); 
    end

    % Convert MATLAB array to NumPy array
    np_input = np.array(input_vector);

    % Reshape to (1, -1) for XGBoost predict
    reshaped_input = np_input.reshape(int32(1), int32(length(input_vector)));

    % Run prediction
    prediction = model.predict(reshaped_input);

    % Convert result to MATLAB scalar
    risk_level = double(prediction.item());  % .item() is safer than {1}
end
