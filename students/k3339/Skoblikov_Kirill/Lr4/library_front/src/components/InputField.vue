<template>
    <div class="input-field">
        <label :for="id" v-if="label">
            {{ label }}
            <span v-if="required" class="required-star"> *</span>
        </label>

        <input
            :type="type"
            :id="id"
            :placeholder="placeholder"
            :required="required"
            :disabled="disabled"
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"
            @blur="$emit('blur')"
        />

        <div v-if="errors && errors.length" class="field-error">
            {{ errors.join(', ') }}
        </div>
    </div>
</template>

<script>
export default {
    name: 'InputField',
    props: {
        label: {
            type: String,
            default: ''
        },
        type: {
            type: String,
            default: 'text'
        },
        id: {
            type: String,
            required: true
        },
        placeholder: {
            type: String,
            default: ''
        },
        required: {
            type: Boolean,
            default: false
        },
        disabled: {
            type: Boolean,
            default: false
        },
        modelValue: {
            type: [String, Number],
            default: ''
        },
        errors: {
            type: Array,
            default: () => []
        }
    },
    emits: ['update:modelValue', 'blur']
}
</script>

<style scoped>
.input-field {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.input-field label {
    color: #555;
    font-weight: 600;
    font-size: 0.95rem;
}

.required-star {
    color: #d32f2f;
}

.input-field input {
    padding: 12px 15px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 16px;
    transition: all 0.3s ease;
    background: #fff;
    font-family: inherit;
}

.input-field input:focus {
    outline: none;
    border-color: #7a66ea;
    box-shadow: 0 0 0 3px rgba(122, 102, 234, 0.1);
}

.input-field input:disabled {
    background: #f5f5f5;
    cursor: not-allowed;
}

.field-error {
    color: #d32f2f;
    font-size: 0.85rem;
    margin-top: 3px;
}
</style>