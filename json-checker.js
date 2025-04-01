const fs = require('fs');
const path = require('path');
const xlsx = require('xlsx'); // Import the xlsx package

// Paths to the JSON files
const oldFilePath = path.join('/home/sheri/Documents/JSON-checker/old/1.json');
const newFilePath = path.join('/home/sheri/Documents/JSON-checker/new/1.json');

// Function to read and parse JSON files
function readJSON(filePath) {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error(`Error reading or parsing file at ${filePath}:`, error);
        return null;
    }
}

// Function to find differences between two JSON objects
function findDifferences(oldJSON, newJSON) {
    const changes = [];
    const keys = new Set([...Object.keys(oldJSON), ...Object.keys(newJSON)]);

    keys.forEach(key => {
        if (JSON.stringify(oldJSON[key]) !== JSON.stringify(newJSON[key])) {
            changes.push({
                key,
                oldValue: oldJSON[key],
                newValue: newJSON[key],
                changeType: oldJSON[key] === undefined
                    ? 'Added'
                    : newJSON[key] === undefined
                    ? 'Removed'
                    : 'Modified',
            });
        }
    });

    return changes;
}

// Function to extract only the values of objects or arrays in a formatted way
function extractValues(value) {
    if (Array.isArray(value)) {
        // If the value is an array, return its elements as a comma-separated string
        return value.map(v => extractValues(v)).join(', ');
    } else if (typeof value === 'object' && value !== null) {
        // If the value is an object, return its values as a comma-separated string
        return Object.values(value).map(v => extractValues(v)).join(', ');
    }
    // For primitive values, return as a string
    return value !== undefined ? value.toString() : 'N/A';
}

// Function to write differences to an Excel file with changes in columns
function writeDifferencesToExcel(differences, outputFilePath) {
    // Prepare data for the worksheet
    const worksheetData = [
        ['Key', 'ChangeType', 'OldValue', 'NewValue'], // Header row
    ];const fs = require('fs');
    const path = require('path');
    const xlsx = require('xlsx'); // Import the xlsx package
    
    // Paths to the JSON files
    const oldFilePath = path.join('/home/sheri/Documents/JSON-checker/old/1.json');
    const newFilePath = path.join('/home/sheri/Documents/JSON-checker/new/1.json');
    
    // Function to read and parse JSON files
    function readJSON(filePath) {
        try {
            const data = fs.readFileSync(filePath, 'utf8');
            return JSON.parse(data);
        } catch (error) {
            console.error(`Error reading or parsing file at ${filePath}:`, error);
            return null;
        }
    }
    
    // Function to find differences between two JSON objects
    function findDifferences(oldJSON, newJSON) {
        const changes = [];
        const keys = new Set([...Object.keys(oldJSON), ...Object.keys(newJSON)]);
    
        keys.forEach(key => {
            if (JSON.stringify(oldJSON[key]) !== JSON.stringify(newJSON[key])) {
                changes.push({
                    key,
                    oldValue: oldJSON[key],
                    newValue: newJSON[key],
                    changeType: oldJSON[key] === undefined
                        ? 'Added'
                        : newJSON[key] === undefined
                        ? 'Removed'
                        : 'Modified',
                });
            }
        });
    
        return changes;
    }
    
    // Function to extract only the values of objects or arrays in a formatted way
    function extractValues(value) {
        if (Array.isArray(value)) {
            // If the value is an array, return its elements as a comma-separated string
            return value.map(v => extractValues(v)).join(', ');
        } else if (typeof value === 'object' && value !== null) {
            // If the value is an object, return its values as a comma-separated string
            return Object.values(value).map(v => extractValues(v)).join(', ');
        }
        // For primitive values, return as a string
        return value !== undefined ? value.toString() : 'N/A';
    }
    
    // Function to write differences to an Excel file with changes in columns
    function writeDifferencesToExcel(differences, outputFilePath) {
        // Prepare data for the worksheet
        const worksheetData = [
            ['Key', 'ChangeType', 'OldValue', 'NewValue'], // Header row
        ];
    
        differences.forEach(diff => {
            worksheetData.push([
                diff.key,
                diff.changeType,
                extractValues(diff.oldValue),
                extractValues(diff.newValue),
            ]);
        });
    
        // Create the worksheet and workbook
        const worksheet = xlsx.utils.aoa_to_sheet(worksheetData); // Use aoa_to_sheet for column-wise data
        const workbook = xlsx.utils.book_new();
        xlsx.utils.book_append_sheet(workbook, worksheet, 'Changes');
    
        // Write the workbook to the file
        xlsx.writeFile(workbook, outputFilePath);
    }
    
    // Main logic
    const oldJSON = readJSON(oldFilePath);
    const newJSON = readJSON(newFilePath);
    
    if (oldJSON && newJSON) {
        const differences = findDifferences(oldJSON, newJSON);
        if (differences.length > 0) {
            console.log('Differences found. Writing to Excel file...');
            const outputFilePath = path.join('/home/sheri/Documents/JSON-checker', 'column-wise-differences.xlsx');
            writeDifferencesToExcel(differences, outputFilePath);
            console.log(`Differences written to ${outputFilePath}`);
        } else {
            console.log('No differences found.');
        }
    }

    differences.forEach(diff => {
        worksheetData.push([
            diff.key,
            diff.changeType,
            extractValues(diff.oldValue),
            extractValues(diff.newValue),
        ]);
    });

    // Create the worksheet and workbook
    const worksheet = xlsx.utils.aoa_to_sheet(worksheetData); // Use aoa_to_sheet for column-wise data
    const workbook = xlsx.utils.book_new();
    xlsx.utils.book_append_sheet(workbook, worksheet, 'Changes');

    // Write the workbook to the file
    xlsx.writeFile(workbook, outputFilePath);
}

// Main logic
const oldJSON = readJSON(oldFilePath);
const newJSON = readJSON(newFilePath);

if (oldJSON && newJSON) {
    const differences = findDifferences(oldJSON, newJSON);
    if (differences.length > 0) {
        console.log('Differences found. Writing to Excel file...');
        const outputFilePath = path.join('/home/sheri/Documents/JSON-checker', 'column-wise-differences.xlsx');
        writeDifferencesToExcel(differences, outputFilePath);
        console.log(`Differences written to ${outputFilePath}`);
    } else {
        console.log('No differences found.');
    }
}