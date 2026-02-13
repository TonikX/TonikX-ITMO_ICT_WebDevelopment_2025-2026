<template>
  <div class="redirect-link">
    <slot></slot>
  </div>
</template>

<script>
export default {
    name: 'RedirectLink'
}
</script>

<style>
.redirect-link {
    text-align: center;
    margin-top: 20px;
    color: #666;
    font-size: 0.95rem;
}

.redirect-link a {
    color: #7a66ea;
    text-decoration: none;
    font-weight: 600;
    margin-left: 5px;
    transition: color 0.3s ease;
}

.redirect-link a:hover {
    color: #6a56da;
    text-decoration: underline;
}
</style>