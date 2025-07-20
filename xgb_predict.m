function risk_level = xgb_predict(input_vector)
    % xgb_predict - MATLAB wrapper to call Python XGBoost model
    % Input: input_vector - 1x10 [v, x, y, brake, steer, a, angle_to_ped, mu, vis, bdist]
    % Output: risk_level - integer in {0, 1, 2}

    persistent model pyLoaded py_np

    if isempty(pyLoaded)
        py.importlib.import_module('joblib');
        py_np = py.importlib.import_module('numpy');
        model = py.joblib.load('xgb_risk_model.pkl');
        pyLoaded = true;
    end

    % Convert MATLAB input to Python numpy array with shape (1, 10)
    py_input_array = py_np.array(input_vector);
    py_input_array = py_input_array.reshape(int32(1), int32(10));

    % Predict class probabilities
    py_pred = model.predict_proba(py_input_array);

    % Convert Python nested list (2D) to MATLAB matrix
    pred_proba_mat = double(py.array.array('d', py_np.nditer(py_pred)));

    % Get class with max probability
    [~, idx] = max(pred_proba_mat);

    risk_level = idx - 1;  % Adjust for MATLAB indexing
end
