/*!
    * Start Bootstrap - Freelancer v6.0.5 (https://startbootstrap.com/theme/freelancer)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
    */
    (function($) {
    "use strict"; // Start of use strict
  
    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
      if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
          $('html, body').animate({
            scrollTop: (target.offset().top - 71)
          }, 1000, "easeInOutExpo");
          return false;
        }
      }
    });
  
    // Scroll to top button appear
    $(document).scroll(function() {
      var scrollDistance = $(this).scrollTop();
      if (scrollDistance > 100) {
        $('.scroll-to-top').fadeIn();
      } else {
        $('.scroll-to-top').fadeOut();
      }
    });
  
    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function() {
      $('.navbar-collapse').collapse('hide');
    });
  
    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
      target: '#mainNav',
      offset: 80
    });
  
    // Collapse Navbar
    var navbarCollapse = function() {
      if ($("#mainNav").offset().top > 100) {
        $("#mainNav").addClass("navbar-shrink");
      } else {
        $("#mainNav").removeClass("navbar-shrink");
      }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
  
    // Floating label headings for the contact form
    $(function() {
      $("body").on("input propertychange", ".floating-label-form-group", function(e) {
        $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
      }).on("focus", ".floating-label-form-group", function() {
        $(this).addClass("floating-label-form-group-with-focus");
      }).on("blur", ".floating-label-form-group", function() {
        $(this).removeClass("floating-label-form-group-with-focus");
      });
    });



    // Subscribe submit
    $("#signupsubmit").click(subscribe)
    // Subscribe submit
    $("#UnsubSubmit").click(unsubscribe)
    // Validate submit
    $("#ValidSubmit").click(validate)
  
  })(jQuery); // End of use strict
  
  function subscribe() {

    // Clear previous error
    $("#signuperror").hide()

    var email = $("#SignupEmail").val();
    var name = $("#SignupName").val();

    var error_message = ""
    
    if (email.length == 0) {
      error_message = "No email supplied"
    }
    else if (name.length == 0) {
      error_message = "No name supplied"
    }
    else if (email.indexOf("@") < 0) {
      error_message = "Doesn't look like an email address"
    }

    if (error_message.length > 0) {
      $("#signuperror").text(error_message);
      $("#signuperror").show();
      return(false);
    }

    var action="signup";

    $.ajax({
      url: "rct.py",
      type: "get",
      data: { 
        "action": action, 
        "email": email, 
        "name": name
      },
      success: function(response) {
        $("#SignupEmail").val("");
        $("#SignupName").val("");
    
        $(".close").click();
        $("#togglevalidate").click();    
      },
      error: function(xhr,options,error) {
        console.log("Got AJAX error "+error)
      }
    });
    // Ignore the submit as a conventional response.
    return false;
  }

  function unsubscribe() {

    // Clear previous error
    $("#unsubscribeerror").hide()
    var error_message = ""
    
    var email = $("#UnsubEmail").val();


    if (email.length == 0) {
      error_message = "No email supplied"
    }
    else if (email.indexOf("@") < 0) {
      error_message = "Doesn't look like an email address"
    }

    if (error_message.length > 0) {
      $("#unsubscribeerror").text(error_message);
      $("#unsubscribeerror").show();
      return(false);
    }

    var action="unsubscribe";
    
    $.ajax({
      url: "rct.py",
      type: "get",
      data: { 
        "action": action, 
        "email": email
      },
      success: function(response) {
        $("#UnsubEmail").val("");
        $(".close").click();
        $("#togglevalidate").click();
      },
      error: function(xhr,options,error) {
        $("#unsubscribeerror").text(error);
        $("#unsubscribeerror").show();
        return(false);
      }
    });
    // Ignore the submit as a conventional response.
    return false;
  }


  function validate() {

    // Clear previous error
    $("#validateerror").hide()
    var error_message = ""
    
    var code = $("#ValidCode").val();

    if (code.length == 0) {
      error_message = "No code supplied"
    }

    if (error_message.length > 0) {
      $("#validateerror").text(error_message);
      $("#validateerror").show();
      return(false);
    }
    
    var action="validate";

    $.ajax({
      url: "rct.py",
      type: "get",
      data: { 
        "action": action, 
        "code": code
      },
      success: function(response) {
        $("#ValidCode").val(""); 
        $(".close").click();
        $("#togglesuccess").click();
      },
      error: function(xhr,options,error) {
        $("#validateerror").text(error);
        $("#validateerror").show();
        return(false);
      }
    });
    // Ignore the submit as a conventional response.
    return false;
  }